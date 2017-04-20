# Project Proposal
## Project Meeting
Office Hours
01:15pm - Thursday, April 27, 2017
Pacific Time - US & Canada
DBH 4204

## Project Summary
We will be making a reinforcement learning AI that takes a flat world of randomly generated lava, reward, and normal blocks as an input. As an output, it will return the shortest route to all the reward blocks that does not touch any lava blocks. The AI will not be given the set of blocks which makes up the world around it. Instead it must find the shortest path by trying out different paths and finding rewards without falling into the lava.

## ML/AI Algorithms
For out project we will use a temporal difference machine learning algorithm. 

## Evaluation Plan
### Quantitative evaluation:
Our primary quantitative metric is the difference between the reward score achieved by the agent, compared to the optimal reward score achieved by using Dijkstra’s algorithm. The reward score will be something like -1 for each move the agent makes, +10 for each reward tile the agent touches, and -100 for touching a lava block. A secondary quantitative metric we will use will be the number of attempts taken to find the optimal path. This will have no baseline, and we improve the score of the metric by optimizing the constants within our algorithm. 
### Baseline
The Baseline will be The average reward of N random paths. We expect our approach to vastly improve from the baseline because the baseline makes completely random decisions and does not learn
### Qualitative analysis:
For our sanity cases we would make sure the path is continuous, and that the agent does not teleport over more than one block at a time. We would also make sure that stepping in each block type yields their respective rewards. We will visualize the internals of our algorithm by printing the expected reward for each action.
