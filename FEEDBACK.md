# Feedback

1. Your team: IG
2. Name of each individual participating: Ian Zhang, Guhan Sivakumar
3. How many unit tests were you able to pass? 13
4. Document and describe any enhancements included to help the judges properly grade your submission.
    - Utilized pandas library to easily filter and work with json data for faster performance
    - Implemented a dynamic REST api that can query data and can execute the functions from simple_data_tool.py, deployable by running `python server.py`
      - List of all functions and headers can be queried at http://localhost:8080/func, i.e. http://localhost:8080/func/get_num_of_open_claims_for_agent_and_severity?agent_id=24&min_severity_rating=1 will return `16`, just like the test case.
      - JSON data can be retrieved directly using `get_x_x_data` accesses, i.e. http://localhost:8080/func/get_claim_handler_data.
    - Implemented a visual map of disasters with optional time filtering. Deployable using `streamlit run streamlit_viz.py`.

5. Any feedback for the coding competition? Things you would like to see in future events?
   - Very fun!
   - Could have used more clarity with documentation

This form can also be emailed to [codingcompetition@statefarm.com](mailto:codingcompetition@statefarm.com). Just make sure that you include a link to your GitHub pull requests.
