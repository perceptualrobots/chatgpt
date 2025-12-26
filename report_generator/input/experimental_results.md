# Experimental Results Notes

## Performance Data

### Visual Media
- **Video** \citep{young2025} : Shows random controller, RL (Symphony) controller, and evolved PCT controller
- **Image**: `RLvPCT-toscale.png`
  - Caption: The RL and PCT networks displayed to scale. The PCT controller is barely visible in comparison.
- **Image**: `PCT.png`
  - Caption: PCT network: 1 level with 6 control units.
  - 6 perceptions simultaneously controlled.
  - The Outputs combine to form environment actions

### Quantitative Results

**Performance comparison**: 100 episodes

Results table from this JSON data:
#### RL Results (Symphony)
```json
{
  "model_details": [
    {"name": "Actor", "total_parameters": 68610, "total_nodes": 514},
    {"name": "Critic", "total_parameters": 267012, "total_nodes": 1284}
  ],
  "total_parameters": 335622,
  "total_nodes": 1798,
  "num_episodes": 100,
  "count=100": 75,
  "count=-100": 5,
  "count=0": 20
}
```


#### PCT Results
```json
{
  "model_details": {
    "total_nodes": 6, 
    "total_parameters": 29,
    "num_episodes": 100,
    "count=100": 79,
    "count=-100": 8,
    "count=0": 13
    }
}
```

## Presentation Elements
- Results summary table
- **Results reproduction**:
  - *TODO*: PCT example, link to code
  - Simphony model - \citep{timurgepard2024github,timurgepard2024youtube}
- Videos
- Key findings and insights

