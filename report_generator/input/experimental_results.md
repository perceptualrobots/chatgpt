# Experimental Results Notes

## Performance Data

### Visual Media
- **Video** (Young, R., 2025): Shows random controller, RL (Symphony) controller, and evolved PCT controller
- **Image**: `G:\My Drive\PR\reports\LunarLander\RLvPCT-toscale.png`
  - RL and PCT networks drawn to scale
  - PCT controller barely visible in comparison
- **Image**: `G:\My Drive\PR\reports\LunarLander\PCT.png`
  - PCT network: 1 level with 6 control units
  - 6 perceptions simultaneously controlled
  - Outputs combine to form environment actions

### Quantitative Results

**Performance comparison**: 100 episodes

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
    "count=-100": 5,
    "count=0": 16
    }
}
```

## Presentation Elements
- Results summary table
- **Results reproduction**:
  - *TODO*: PCT example, link to code
  - Simphony model - *include reference*
- Videos
- Key findings and insights

