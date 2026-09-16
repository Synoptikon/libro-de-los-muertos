# Source Verification Gate

The gate requires exact equality between registered and observed `source_id` and `inventory_number`, plus an absolute HTTP(S) URI. It does not download content, calculate hashes, or assert authenticity. Successful identity matching returns `VERIFIED`.

Transition: `REGISTERED_REFERENCE -> VERIFIED_IDENTITY -> ACQUISITION`.
