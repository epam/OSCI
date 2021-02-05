import azure.durable_functions as df


def orchestrator_function(context: df.DurableOrchestrationContext):
    uri = context.get_input()
    result = yield context.call_http('GET', uri=uri)
    return [result, ]


main = df.Orchestrator.create(orchestrator_function)
