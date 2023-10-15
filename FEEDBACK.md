# Feedback

1. Your team: Preston Roesslet
2. Name of each individual participating: Preston Roesslet
3. How many unit tests were you able to pass?
4. Document and describe any enhancements included to help the judges properly grade your submission.

   I implemented a REST Api to interact with the data from the problem set. I utilized Spring Boot.

   The Spring Boot application runs from the RestApi class. I then created all of the endpoints inside of the RestEntryPoint.java file.

   To run the Spring Boot application, run `mvn spring-boot:run`. It runs on localhost:8080 and below are a list of the available endpoints:

   - /numberClosedClaims - returns the number of claims where the status is closed
   - /numClaims/{id} - returns the number of claims associated with the given claim handler ID
   - /numDisasters/{state} - returns the number of disasters in the given state
   - /disasterTotalCost/{id} - returns the total claim cost for the given disaster ID

5. Any feedback for the coding competition? Things you would like to see in future events?
   One thing in particular that I think could be better is ensuring that the test cases and skeleton code are bug free. While I know that programming certainly comes along with bugs, it felt as though there were many issues, some of which weren't being resolved until towards the end of the competition.

This form can also be emailed to [codingcompetition@statefarm.com](mailto:codingcompetition@statefarm.com). Just make sure that you include a link to your GitHub pull requests.
