# Experimental Results Notes

## Performance Data


### PCT process

The evolutionary PCT process converged to a system with only one level, with 6 control units.

### Computational Comparison

The RL controller implements a high-dimensional mapping between state and action a relatively enormous network is necessary as shown in the comparative image \ref{fig:RLvPCT-toscale} where the PCT controller is barely visible. The PCT network, shown in the other image \ref{fig:PCT}, which dynamically adjusts action to maintain perceptual inputs is just 6 control units and has significantly fewer weights, by a factor of 10,000.

### Visual Media
- **Video** \citep{young2025} : Shows random controller, RL (Symphony) controller, and evolved PCT controller
- **Image**: `RLvPCT-toscale.png`
  - [width=1.0\textwidth]
  - Caption: The RL and PCT networks displayed to scale. The PCT controller is barely visible in comparison.
  - Label: `RLvPCT-toscale`
- **Image**: `PCT.png`
  - Caption: PCT network: 1 level with 6 control units.
  - Label: `PCT`
  - 6 perceptions simultaneously controlled.
  - The Outputs combine to form environment actions

### Quantitative Results

**Performance comparison **: 100 episodes

Over 100 episodes, the PCT controller achieved a success rate of 79\%, marginally outperforming the RL controller, which had a success rate of 75\%. Despite having significantly fewer parameters — 29 compared to the RL's 335,622 — the PCT controller maintained robust performance metrics, demonstrating its capability to achieve successful landings (100 episodes with a score of 100 indicating success, -100 (failure) a crash, and 0 (neutral) an incomplete landing). The comparative metrics are summarized in the table \ref{tab:results_table}.

- **Table:** Comparative results for RL and PCT. A score of 100 indicates a successful landing, -100 a crash and 0 is incomplete landing at end of run. The PCT network has significantly fewer weights, by a factor of 10,000.
  **Label:** results_table

  | Metric | RL (Symphony) | PCT |
  |--------|---------------|-----|
  | Total Parameters | 335,622 | 29 |
  | Total Nodes | 1,798 | 6 |
  | Success Rate (count=100) | 75 | 79 |
  | Failure Rate (count=-100) | 5 | 8 |
  | Neutral Rate (count=0) | 20 | 13 |



## Presentation Elements
- Results summary table
- **Results reproduction**:
  - PCT results
    - The results of this experiment can be run with the code from the pct Python library \citep{young2026}.
    - Code:
      ```
      PCTExamples.run_example('testfiles/LunarLander/
      LunarLander-4905d2.properties', render=True)
      ```

  - Simphony model - \citep{ishuov2024}
- Videos
- Key findings and insights
- Future work will focus on reproducing these results and further exploring the potential of PCT in other dynamic systems.