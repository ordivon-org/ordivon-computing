# A — Provider-variant sensitivity

Question: is the previously observed operation-specific reconstruction value of the explicit Result/Value map stable across another current DeepSeek model variant?

This track does **not** pre-label one model as more capable. Current official Chat API and current Harness support both `deepseek-v4-flash` and `deepseek-v4-pro`. A transport/schema feasibility probe established `deepseek-v4-pro` works through the same current Harness adapter and credential scope.

Frozen semantic inputs are exactly the earlier post-primary composite workload:

- Book SHA-256 `10ed267c4b4eb9d90bf8b45c65c73482d40aae2d91e7359cbeedaeac37bf782c`;
- map SHA-256 `b3da56b021c973f4a6f1b49d19eb6c3d4039670894e11ff29416a600eb7304c2`;
- composite cases SHA-256 `2b2eeb5f27b637e0e36d9c84983185b04ada98000c653f4c0a697edd851b7671`.

Existing `deepseek-v4-flash` evidence is reused rather than rerun because those exact semantic inputs and Harness revision are unchanged. New evidence runs three fresh `deepseek-v4-pro` replicates per arm under the same non-thinking adapter, zero Tools and structured result contract.

Interpretation:

- compare each model variant internally as `Book` vs `Map+Book`;
- compare observed baseline/treatment error profiles across variants;
- call a variant empirically stronger/weaker **only for this frozen workload** if repeated performance supports it;
- no universal capability ranking or cost-quality claim follows.
