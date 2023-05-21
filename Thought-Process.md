# Form Management System

## Tables

- **Form**
    
    ```markdown
    - id (PK)
    - uid
    - title
    - description
    - state
    - author
    - commands
    - metadata
    - created_at
    - updated_at
    ```
    
- **Question**
    
    ```markdown
    - id (PK)
    - uid
    - title
    - description
    - type
    - rank
    - is_required
    - form_id (FK to Form.id)
    - metadata
    - created_at
    - updated_at
    ```
    
- **Option**
    
    ```markdown
    - id (PK)
    - text
    - question_id (FK to Question.id)
    ```
    
- **Response**
    
    ```markdown
    - id (PK)
    - uid
    - form_id (FK to Form.id)
    - respondent_name
    - respondent_email
    - respondent_phone
    - response_status
    - metadata
    - created_at
    - updated_at
    ```
    
- **Answer**
    
    ```markdown
    - id (PK)
    - question_id (FK to Question.id)
    - response_id (FK to Response.id)
    - value
    ```
    

## APIs

- **Create Form**
    
    ```markdown
    REQUEST
    POST {{url}}/forms/
    {
        "title": "First Form",
        "description": "My First form",
        "commands": "GOOGLESHEET,SMS"
    }
    
    RESPONSE:
    {
        "uid": "6efa4d02-9523-4a1f-8740-6de012a46e01",
        "title": "Second Form",
        "description": "My Second form",
        "state": 1,
        "author": 1,
        "commands": "GOOGLESHEET",
        "created_at": "2023-05-07T21:57:51.659443Z",
        "updated_at": "2023-05-07T21:57:51.659640Z"
    }
    
    // For simplicity, I have used one user in the code from which I can create forms but the forms can be created from multiple users too.
    ```
    
- **Get Form Details**
    
    ```markdown
    REQUEST
    GET {{url}}/forms/{formUID}/
    RESPONSE:
    [
        {
            "uid": "6efa4d02-9523-4a1f-8740-6de012a46e01",
            "title": "Second Form",
            "description": "My Second form",
            "state": 1,
            "author": 1,
            "commands": "GOOGLESHEET",
            "created_at": "2023-05-07T21:57:51.659443Z",
            "updated_at": "2023-05-07T21:57:51.659640Z"
        }
    ]
    ```
    
- **Add Questions in a form**
    
    ```markdown
    REQUEST
    POST {{url}}/forms/{formUID}/questions/
    {
        "title": "First question",
        "description": "First Question",
        "type": "Text",
        "metadata": {}
    }
    
    RESPONSE:
    {
        "status": "S001",
        "message": "Success"
    }
    ```
    
- **Get All Questions**
    
    ```markdown
    REQUEST
    GET {{url}}/forms/{formUID}/questions/
    
    RESPONSE:
    [
        {
            "uid": "22901cfa-8e38-49fc-8102-148dfa52ff63",
            "title": "First question",
            "description": "First Question",
            "rank": 1,
            "type": "Text",
            "metadata": {},
            "created_at": "2023-05-07T21:59:02.927364Z",
            "updated_at": "2023-05-07T21:59:02.927426Z"
        }
    ]
    ```
    
- **Publish a Form**
    
    ```markdown
    REQUEST
    POST {{url}}/forms/{formUID}/publish/
    
    RESPONSE:
    {
        "link": "https://fms.com/forms/6efa4d02-9523-4a1f-8740-6de012a46e01"
    }
    ```
    
- **Submit Answer**
    
    ```markdown
    REQUEST
    POST {{url}}/forms/{formUID}/submit-answers/
    {
        "respondent_name": "Test Name",
        "respondent_email": "test@gmail.com",
        "respondent_phone": "1234567895",
        "metadata": {},
        "answers": [
            {
                "question_uid": "22901cfa-8e38-49fc-8102-148dfa52ff63",
                "value": "answer 1"
            }
        ]
    }
    
    RESPONSE:
    {
        "status": "S001",
        "message": "Success"
    }
    ```
    

There can be several APIs that can be written here but for simplicity I have used only the above APIs for MVP. Examples of other APIs: 

1. Get all Forms Created by a user
2. Get all submissions by a user

Etc

## Benchmarking and Monitoring

To benchmark the system, we can use tools like Apache **JMeter** or **Gatling**. We can simulate various traffic patterns and measure the system's response time, throughput, and error rate.

To monitor the system's health, we can use tools like **Nagios** or **Zabbix**. We can monitor the system's CPU usage, memory usage, disk usage, network traffic, and service availability. We can also use **New-Relic** for tracking the time taken by each api/function in the code. We can also set up alerts to notify us when the system health is affected.

The errors can be tracked over S**entry**, I have used the function `submit_exception_on_sentry(error)` if any unexpected error occurs.

I have also used **PyLint** for static type checking of errors.

The unit test cases should also be written for validating each scenario. I have skipped writing those test cases for now.

## Logging

To log system events, we can use a centralized logging system like Elasticsearch, Logstash, and Kibana (ELK). We can log system events like response submissions, database updates, Google Sheets updates, plugin executions, and error messages. The logs can help us troubleshoot issues and optimize system performance.

## Code Formatting

For code Formatting, I have used **Black**, **iSort** and **flake8**. These help in formatting the code and also help in maintaining production level code.

These have been integrated with the help of **pre-commit** library. This helps in formatting all the files and pointing out all the basic formatting errors in the code before committing the files.

## Plug & Play System

I have implemented the Google Sheets for plug and play. In the same fashion every other system can be implemented and the command can be given in the forms itself.

## Data Validation

There are different types of validation that can be performed on the answers to ensure they conform to the question metadata. Here are a few examples:

1. Data type validation: This ensures that the data entered in the response matches the expected data type. For example, if a question expects a numerical value, the answer should be a number and not a string.
2. Range validation: This ensures that the data entered in the response falls within an acceptable range. For example, if a question asks for the age of a person, it should be within a reasonable range, such as 0 to 120 years.
3. Format validation: This ensures that the data entered in the response matches a specific format. For example, if a question asks for an email address, the answer should follow a specific format, such as "**[username@domain.com](mailto:username@domain.com)**".
4. Consistency validation: This ensures that the data entered in the response is consistent with other data entered in the form. For example, if a form has multiple questions about a person's name, the answers should be consistent across all questions.

These validations can be performed on the client-side using JavaScript or on the server-side using Django's form validation functionality.

For simplicity, I have assumed these validations to be done on client side. and hence not written in the code except some simple validations which can be extended for further validations.

## Conclusion

To support post-submission business logic for data collected via Collect, we can design a modular system with a unified interface acting as a middleman. The system can use a relational database for data storage, integrate with third-party services like Google Sheets, and have a plugin architecture to support multiple use cases.

### Pros:

- The proposed approach allows for the easy integration of new use cases without needing an overhaul of the backend. This is achieved by having a unified interface acting as a middleman.
- The design accounts for eventual consistency and ensures that no responses are missed in the journey.
- The design is failsafe and can recover from circumstances like power/internet/service outages.
- The proposed data storage schema is flexible and can easily scale to millions of responses across hundreds of forms for an organization.
- The logging and monitoring setup ensures that system health can be tracked and alerts can be triggered when there are issues.

### Cons:

- One potential downside of this approach is that it requires a significant upfront investment in terms of designing the system architecture and building the infrastructure to support it.
- The use of third-party services, such as Google Sheets, may introduce additional limitations and constraints that need to be considered and accounted for in the design if done synchronously. The better approach for doing this would be using a queue service such as **SQS**.