create index if not exists masamune_review_receipt_delivery_id_idx
    on public.masamune_review_receipt (delivery_id);

comment on index public.masamune_review_receipt_delivery_id_idx is
    'Covers the delivery foreign key for receipt maintenance and future delivery cleanup.';
