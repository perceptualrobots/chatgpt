# Experimental Results Notes

## Performance Data

### Computational Comparison

The RL controller implements a high-dimensional mapping between state and action an enormous network, relatively, is necessary as shown in the first image where the PCT controller is barely visible. The PCT network, shown in the second image, which dynamically adjusts action to maintain perceptual inputs is just 6 control units and has significantly fewer weights, by a factor of 10,000.

### Visual Media
- **Video** \citep{young2025} : Shows random controller, RL (Symphony) controller, and evolved PCT controller
- **Image**: `RLvPCT-toscale.png`
  - [width=1.0\textwidth]
  - Caption: The RL and PCT networks displayed to scale. The PCT controller is barely visible in comparison.
- **Image**: `PCT.png`
  - Caption: PCT network: 1 level with 6 control units.
  - 6 perceptions simultaneously controlled.
  - The Outputs combine to form environment actions

### Quantitative Results

**Performance comparison **: 100 episodes


| Metric | RL (Symphony) | PCT |
|--------|---------------|-----|
| Total Parameters | 335,622 | 29 |
| Total Nodes | 1,798 | 6 |
| Success Rate (count=100) | 75 | 79 |
| Failure Rate (count=-100) | 5 | 8 |
| Neutral Rate (count=0) | 20 | 13 |

Table: Comparative results for RL and PCT. A score of 100 indicates a successful landing, -100 a crash and 0 is incomplete landing at end of run.



## Presentation Elements
- Results summary table
- **Results reproduction**:
  - *TODO*: PCT example, link to code
  - Simphony model - \citep{ishuov2024}
- Videos
- Key findings and insights

