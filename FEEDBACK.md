# Feedback

1. Your team: Preston Roesslet
2. Name of each individual participating: Preston Roesslet
3. How many unit tests were you able to pass? 13 - However, I believe that I would pass all 14 of them if Issue #9 had been resolved. At the time of my submission, Issue #9 had yet to be resolved.
4. Document and describe any enhancements included to help the judges properly grade your submission.

   I implemented a REST Api to interact with the data from the problem set. I utilized Spring Boot. The Spring Boot application is initialized in the RestApi class. I then created all of the endpoints inside of the ApiController.java file.

   To run the Spring Boot application, run `mvn spring-boot:run`. The required packages have already been added to my pom.xml file. It runs on localhost:8080 and below is a list of the available endpoints:

   - /numberClosedClaims - returns the number of claims where the status is closed
   - /numClaims/{id} - returns the number of claims associated with the given claim handler ID
   - /numDisasters/{state} - returns the number of disasters in the given state
   - /disasterTotalCost/{id} - returns the total claim cost for the given disaster ID
   - /averageClaimCost/{id} - returns the average claim cost for the given claim handler ID
   - /stateWithMostDisasters - returns the state with the highest number of disasters
   - /stateWithLeastDisasters - returns the state with the highest number of disasters
   - /mostSpokenLanguage/{state} - returns the language spoken most by claim handlers in the given state
   - /numOpenClaims/{id}/{minSeverity} - returns the number of open claims for the given agent ID and above the given minimum severity
   - /numDistastersDeclaredAfterEndDate - returns the number of disasters where it was declared after it ended
   - /agentsTotalClaimCost - returns a map of agent ID's and their total claim cost
   - /disasterClaimDensity/{id} - returns the density of the given disaster ID based on the number of claims and the impact radius

   This could be further extended to include persistent data through a database rather than just json files, or even creating a front end to view/edit the data. However, given the time constraints for this competition, these were not feasible to implement.

5. Any feedback for the coding competition? Things you would like to see in future events?

   One thing in particular that I think could be better is ensuring that the test cases and skeleton code are bug free. While I know that programming certainly comes along with bugs, it felt as though there were many issues, some of which weren't being resolved until towards the end of the competition. This made it difficult to complete all tasks in an efficient manner and I could not complete one of the test cases at all prior to submission due to this.

   Overall though this was a very fun competition!

This form can also be emailed to [codingcompetition@statefarm.com](mailto:codingcompetition@statefarm.com). Just make sure that you include a link to your GitHub pull requests.
