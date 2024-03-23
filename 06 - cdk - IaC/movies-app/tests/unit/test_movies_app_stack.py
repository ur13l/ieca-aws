import aws_cdk as core
import aws_cdk.assertions as assertions

from movies_app.movies_app_stack import MoviesAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in movies_app/movies_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MoviesAppStack(app, "movies-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
