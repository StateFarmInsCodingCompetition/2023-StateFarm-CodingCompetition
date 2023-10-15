# Unit Test Ideas

**Make sure to specify that there are 50 states plus the District of Columbia!!**

## Given

- [x] Can read each JSON file

## Easy

- [x] Get number of closed claims
- [x] Can get the number of claims assigned to a claim handler
- [x] Get number of disasters for a specific state

## Medium

- [x] For a specific disaster, calculate total cost from claims
- [x] For a specific claim handler, calculate the average cost of claims they're assigned to
- [x] Get states with the most and least disasters
- [x] Most spoken language by agents in a specific state
- Get number of open claims for a specific agent based on severity rating
<!-- - Get agent with lowest total claim cost
- Get agent with highest average claim cost -->
<!-- - Get disaster with the least amount claim severity -->

## Hard

- Get the number of disasters where the disaster was declared after the end date
- Return four lists of claims where:
  - The agent assigned is in the Northeast OR West regions
  - AND the disaster was declared between 2023-01-01 to 2023-05-31 (inclusive).
  - Lists of claims are split up by:
    - claim has loss_of_life = true, but total_loss = false
    - claim has loss_of_life = false, but total_loss = true
    - claim has loss_of_life and total_loss as true
    - claim has loss_of_life and total_loss as false
- Build map of agents to their total claim cost
- Calculate the density of claims for a particular disaster
  - Leverage claims and disaster's radius
  - Would have to find the area of a circle :O

## Godmode

- Get month with highest total claim cost
  - Disaster declared date + claim costs
  - Return month as "January" instead of "01" for example
- Categorize each disaster based on the following criteria:
  - TODO see if possible or too difficult
  - stat = ((Total claim co
  - st * disaster radius) / (Number of claims - Number of claims w/ total losses and loss of life)) * duration (end date - start date in days, inclusive)
  - We'd have to try this out so we could figure out a scale. could be like:
      - Have them order the disaster list from lowest stat to highest and say:
      - first 40 are Category 1
      - next 20 are Category 2
      - next 18 are Category 3
      - next 7 are Category 4
      - last 5 are Category 5
