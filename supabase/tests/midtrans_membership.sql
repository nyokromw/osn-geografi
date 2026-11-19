-- No real customer rows are used. All fixtures and changes are rolled back.
begin;
do $$
declare
  student uuid := gen_random_uuid();
  administrator uuid := gen_random_uuid();
  other_student uuid := gen_random_uuid();
  premium integer;
  platinum integer;
  order_data jsonb;
  order_id_value text;
  late_order_id text;
  payment public.pembayaran_midtrans%rowtype;
  old_expiry timestamp;
  new_expiry timestamp;
  current_status text;
  row_count integer;
begin
  insert into auth.users (id, email, raw_user_meta_data) values
    (student, 'qris-test-' || student::text || '@example.invalid', '{}'::jsonb),
    (administrator, 'qris-test-' || administrator::text || '@example.invalid', '{}'::jsonb),
    (other_student, 'qris-test-' || other_student::text || '@example.invalid', '{}'::jsonb);
  update public.profiles set role = 'admin' where id = administrator;
  select id into premium from public.paket_membership where akses = 'premium' and durasi_hari = 30 and aktif is true limit 1;
  select id into platinum from public.paket_membership where akses = 'platinum' and durasi_hari = 30 and aktif is true limit 1;
  if premium is null or platinum is null then raise exception 'Test requires active monthly plans'; end if;

  if has_function_privilege('authenticated', 'public.midtrans_create_order(uuid,integer,text)', 'EXECUTE')
     or has_function_privilege('anon', 'public.midtrans_reconcile_order(text,text,numeric,text,text,text,text,text,text)', 'EXECUTE')
     or has_table_privilege('authenticated', 'public.pembayaran_midtrans', 'UPDATE')
     or has_table_privilege('anon', 'public.pembayaran_midtrans', 'SELECT') then
    raise exception 'Payment write privileges leaked to a browser role';
  end if;

  begin
    perform public.midtrans_create_order(student, premium, 'sandbox');
    raise exception 'Student should not create a sandbox order';
  exception when others then
    if sqlerrm not like 'Simulasi pembayaran hanya%' then raise; end if;
  end;
  begin
    perform public.midtrans_create_order(student, premium, 'prod');
    raise exception 'Invalid environment accepted';
  exception when others then
    if sqlerrm not like 'Lingkungan pembayaran tidak valid%' then raise; end if;
  end;

  order_data := public.midtrans_create_order(student, premium, 'production');
  order_id_value := order_data->'order'->>'order_id';
  if (public.midtrans_create_order(student, premium, 'production')->'order'->>'order_id') <> order_id_value then
    raise exception 'Repeated checkout did not reuse the open order';
  end if;
  payment := public.midtrans_reconcile_order(order_id_value, 'production',
    (order_data->'order'->>'nominal')::numeric, gen_random_uuid()::text, 'qris', 'pending', '201', null, 'IDR');
  select status into current_status from public.profiles where id = student;
  if current_status <> 'gratis' then raise exception 'Pending payment activated membership'; end if;
  begin
    perform public.midtrans_reconcile_order(order_id_value, 'production', 1,
      payment.midtrans_transaction_id, 'qris', 'settlement', '200', null, 'IDR');
    raise exception 'Wrong amount accepted';
  exception when others then
    if sqlerrm not like 'Data pembayaran tidak cocok%' then raise; end if;
  end;
  payment := public.midtrans_reconcile_order(order_id_value, 'production', payment.nominal,
    payment.midtrans_transaction_id, 'qris', 'settlement', '200', 'accept', 'IDR');
  select status, status_expired into current_status, old_expiry from public.profiles where id = student;
  if current_status <> 'premium' or old_expiry < timezone('UTC', now()) + interval '29 days 23 hours'
    or payment.fulfilled_at is null then raise exception 'Paid order did not activate Premium'; end if;
  perform public.midtrans_reconcile_order(order_id_value, 'production', payment.nominal,
    payment.midtrans_transaction_id, 'qris', 'settlement', '200', 'accept', 'IDR');
  perform public.midtrans_reconcile_order(order_id_value, 'production', payment.nominal,
    payment.midtrans_transaction_id, 'qris', 'pending', '201', null, 'IDR');
  select status_expired into new_expiry from public.profiles where id = student;
  if new_expiry <> old_expiry or (select status from public.pembayaran_midtrans where order_id = order_id_value) <> 'paid' then
    raise exception 'Duplicate/regressive notifications changed fulfillment';
  end if;

  order_data := public.midtrans_create_order(student, premium, 'production');
  payment := public.midtrans_reconcile_order(order_data->'order'->>'order_id', 'production',
    (order_data->'order'->>'nominal')::numeric, gen_random_uuid()::text, 'qris', 'settlement', '200', null, 'IDR');
  select status_expired into new_expiry from public.profiles where id = student;
  if new_expiry <> old_expiry + interval '30 days' then raise exception 'Renewal lost remaining days'; end if;

  order_data := public.midtrans_create_order(student, premium, 'production');
  late_order_id := order_data->'order'->>'order_id';
  order_data := public.midtrans_create_order(student, platinum, 'production');
  payment := public.midtrans_reconcile_order(order_data->'order'->>'order_id', 'production',
    (order_data->'order'->>'nominal')::numeric, gen_random_uuid()::text, 'qris', 'settlement', '200', null, 'IDR');
  select status, status_expired into current_status, old_expiry from public.profiles where id = student;
  if current_status <> 'platinum' or old_expiry <> timezone('UTC', now()) + interval '30 days' then
    raise exception 'Upgrade did not start a new Platinum term';
  end if;
  select * into payment from public.pembayaran_midtrans where order_id = late_order_id;
  payment := public.midtrans_reconcile_order(late_order_id, 'production', payment.nominal,
    gen_random_uuid()::text, 'qris', 'settlement', '200', null, 'IDR');
  select status, status_expired into current_status, new_expiry from public.profiles where id = student;
  if current_status <> 'platinum' or new_expiry <> old_expiry or payment.status <> 'review' then
    raise exception 'Late lower-tier payment downgraded an active Platinum account';
  end if;
  begin
    perform public.midtrans_create_order(student, premium, 'production');
    raise exception 'Active Platinum account can buy Premium';
  exception when others then
    if sqlerrm not like 'Platinum masih aktif%' then raise; end if;
  end;

  order_data := public.midtrans_create_order(administrator, premium, 'sandbox');
  payment := public.midtrans_reconcile_order(order_data->'order'->>'order_id', 'sandbox',
    (order_data->'order'->>'nominal')::numeric, gen_random_uuid()::text, 'qris', 'settlement', '200', null, 'IDR');
  select status, status_expired into current_status, new_expiry from public.profiles where id = administrator;
  if current_status <> 'gratis' or new_expiry is not null or payment.fulfilled_at is not null or payment.status <> 'paid' then
    raise exception 'Sandbox changed real membership';
  end if;

  order_data := public.midtrans_create_order(other_student, premium, 'production');
  payment := public.midtrans_reconcile_order(order_data->'order'->>'order_id', 'production',
    (order_data->'order'->>'nominal')::numeric, gen_random_uuid()::text, 'qris', 'expire', '407', null, 'IDR');
  if payment.status <> 'expired' then raise exception 'Expiry was not recorded'; end if;
  select status into current_status from public.profiles where id = other_student;
  if current_status <> 'gratis' then raise exception 'Expired order activated membership'; end if;

  perform set_config('request.jwt.claims', jsonb_build_object('sub', other_student, 'role', 'authenticated')::text, true);
  execute 'set local role authenticated';
  select count(*) into row_count from public.pembayaran_midtrans where user_id <> other_student;
  if row_count <> 0 then raise exception 'Student could see another customer payment'; end if;
  execute 'reset role';

  select * into payment from public.pembayaran_midtrans where user_id = student and status = 'paid' limit 1;
  payment := public.midtrans_reconcile_order(payment.order_id, payment.environment, payment.nominal,
    payment.midtrans_transaction_id, 'qris', 'refund', '200', null, 'IDR');
  if payment.status <> 'refunded' or payment.review_reason is null then raise exception 'Refund review missing'; end if;
end;
$$;
rollback;
select 'PASS: ownership, role grants, sandbox isolation, server-priced checkout, pending, amount mismatch, activation, duplicate/regressive events, renewal, upgrade, downgrade prevention, expiry, refund review; all fixtures rolled back.' as result;
