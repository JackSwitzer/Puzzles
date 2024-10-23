# October 2024 Jane Street Puzzle - "Path Scoring Puzzle" 

This directory contains my solution to the **October 2024 Jane Street Puzzle**. The puzzle involves determining optimal paths and computing scores based on the paths taken through a grid with values and operations applied along the way.

Link to the puzzle: [October 2024 Jane Street Puzzle](https://www.janestreet.com/puzzles/current-puzzle/)

## Final Solution

I was able to validate and complete the solution for this puzzle. Below is the output and a visualization of the path used in my final solution.

### Solution
#### Path:
1,3,2,a1,c2,a3,c4,d6,b5,d4,f3,e5,c6,a5,b3,d2,e4,f6,a6,c5,d3,b4,a2,c3,e2,f4,d5,b6,a4,b2,d1,e3,f1

#### Grid:
![Final Solution Vis.](https://github.com/JackSwitzer/Jane-Street-Puzzles/blob/main/October%202024/photos/Final%20Solution%20Vis.png?raw=true)



## Optimal Solution
- TBD

## Methodology
### Overview
The objective was to find paths that yielded a final score of 2024 while optimizing the operations between grid elements.

### Step-by-Step Process

#### Initial Modeling (30 minutes):
- I started by modeling the grid and designing the knight movement class to simulate the puzzle’s movement rules. This helped visualize the different ways paths could be taken through the grid, while considering how operations applied between steps would affect the final score.
- Used an initial puzzle solving methodology of a brute force check every path and every number simultaniously (very inefficient)
##### Tool: OpenAI Canvas (ChatGPT 4o)


#### Identifying Inefficiencies & Refactoring (75 minutes):
##### Attempt 1: GPU Implementation, Failure (45 minutes):
I attempted to implement GPU processing for the pathfinding algorithms, intending to speed up the search for optimal paths. However, I encountered configuration issues that delayed progress. Ultimately, I reverted to CPU-based solutions, which were sufficient after Attempt 2.
###### Tool: Custom Cuda applications with NVIDIA Cuda Toolkit & numba (Cursor IDE: With OpenAI's o1 & Claude 3.5 Sonnet)

##### Attempt 2: More Optimal Approach, Success (30 minutes):
After testing, I identified inefficiencies in solving for both optimal paths and values concurrently. 
I refactored the process by first focusing on finding the optimal paths without considering A, B, and C. Once paths were identified, I then applied values for A, B, and C to determine the final score. This reduced the complexity significantly.
###### Tool: Cursor IDE (With OpenAI's o1 & Claude 3.5 Sonnet)


#### Testing & Validation (5 minutes):
After implementing the refactored solution, I quickly tested the solution against various cases to ensure that the final score was 2024 and that the paths found were indeed optimal.


#### Visualization (60 minutes):
Finally, I generated a visualization of the optimal path for clarity and to show how the grid was navigated to reach the final score of 2024. This helped ensure the solution was easy to understand and verify.
Total Time Spent

The entire process took approximately 3 hours

### Incorrect Solution
Originally had an issue with the original board set up, fixed and rerun with greater depth for my search to get a more optimal (possibly correct) solution
Old Path: 1,2,22,a1,c2,d4,b5,d6,f5,e3,d5,f6,a6,b4,d3,c5,b3,d2,f1
