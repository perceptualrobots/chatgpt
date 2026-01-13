# Discussion Notes

## PCT Advantages
- **Interpretability**: Break down into control units
- **Biological plausibility**
- **Psychologically credible**
- **Smaller computational footprint**

## RL Advantages
- **Sample efficiency**
- **Generalization**
- **Scalability**

## Analysis Points
- **Comparative analysis**: Strengths and weaknesses of each approach
    - Furthermore, as PCT is not reliant on large datasets, as is RL, PCT, and its small footprint, is likely to result in superior scalability across diverse environments.
    - as PCT is known for dynamic adaptability it is not unexpected to find that the PCT controller is resilient to variations in initial conditions, which may be attributed to its inherent stability and focus on perceptual variables rather than raw state inputs. 

- **Trade-offs** between approaches
    - Based on this study RL does not provide any advantages over PCT.
- **Implications** for real-world applications
- **Limitations** of current study
    - The exploration of PCT in the Lunar Lander environment is still nascent, and further research is required to fully understand its capabilities and limitations. However, its hierarchical and modular nature suggests PCT is scalable to large and complex environments.
    - The PCT controller is not sensitivity to initial configurations.
- **Unexpected findings** and their explanations
    - due to PCT's inherent corrective nature it is not unexpected to find the footprint is smaller than RL though it is unexpected to find such significantly fewer parameters, by a factor of 10,000.
    - as PCT is known for dynamic adaptability it is not unexpected to find that the PCT controller is resilient to variations in initial conditions, which may be attributed to its inherent stability and focus on perceptual variables rather than raw state inputs. 

