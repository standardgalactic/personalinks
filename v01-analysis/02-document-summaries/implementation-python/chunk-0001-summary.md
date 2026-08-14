**Question:**  
What is the purpose of the `update_saturation_bookkeeping` function in the [K
given code, and how does it interact with other parts of the simulation?

**Answer:**  
The `update_saturation_bookkeeping` function serves to track saturation eve[3D[K
events for each scope within a simulated field. Its primary responsibilitie[15D[K
responsibilities are:

1. **Calculate Local Maximum Gain:** For every scope, it computes `local_ma[9D[K
`local_max`, which is the maximum gain achievable through any of the action[6D[K
actions "BIND", "REFUSE", "COLLAPSE", or "POP". This value is appended to t[1D[K
the scope's `gains_over_time` list.

2. **Detect Saturation:** It checks if `local_max` falls below a predefined[10D[K
predefined threshold (`EPSILON`). If this condition is met, it increments t[1D[K
the scope’s `local_saturation_steps` counter and records the current time s[1D[K
step `t` as the start of an active saturation episode by setting `scope.act[10D[K
`scope.active_saturation_start = t`. This indicates that the scope has ente[4D[K
entered a saturated state.

3. **Terminate Saturation Episodes:** When a non-saturated gain is observed[8D[K
observed (i.e., `local_max > EPSILON`) and the scope was previously in satu[4D[K
saturation (`active_saturation_start` is not None), it records the duration[8D[K
duration of the saturation episode by appending `(t - active_saturation_sta[21D[K
active_saturation_start)` to the scope’s `recovery_latencies` list. It then[4D[K
then resets `active_saturation_start` to `None`, marking the end of the cur[3D[K
current saturation period.

**Interaction with Other Parts:**

- **`simulate` Function:** Calls `update_saturation_bookkeeping` in each it[2D[K
iteration of its main loop, ensuring that saturation bookkeeping is updated[7D[K
updated for all scopes at every time step. This integration allows the simu[4D[K
simulation to monitor and record when a scope becomes saturated or exits sa[2D[K
saturation, which influences subsequent actions (e.g., recovery latency cal[3D[K
calculations).

- **Field Saturation Check:** The function indirectly contributes to detect[6D[K
detecting field-wide saturation by tracking individual scope saturations (`[2D[K
(`field_saturated` is called after each update). If all scopes are saturate[8D[K
saturated at a given time step, the simulation increments `field_saturation[17D[K
`field_saturation_steps`, indicating prolonged overall field saturation.

- **Policy Evaluation Metrics:** Through its bookkeeping of recovery latenc[6D[K
latencies and saturation steps, it provides data used to compute metrics li[2D[K
like "time_in_field_saturation", "mean_recovery_latency_after_switch", and [K
"long_horizon_starvation_rate" within the simulation results. These metrics[7D[K
metrics are essential for assessing policy performance based on how scopes [K
handle saturation.

Overall, `update_saturation_bookkeeping` is crucial for monitoring dynamic [K
changes in scope states due to saturation events, enabling a deeper analysi[7D[K
analysis of how different policies influence field behavior under such cond[4D[K
conditions.

