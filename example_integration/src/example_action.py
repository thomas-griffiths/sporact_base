from sporact_base.sporact_base_action import SporactBaseAction


class ExampleAction(SporactBaseAction):

    # Sporact will invoke the run method with the inputs listed in integration.json for every action that is
    # added to a playbook
    def run(self, example_input):

        # The run method of an action must return the outputs declared in integration.json
        # or it must raise an exception if it cannot return the outputs
        return {
            "example_output": example_input,
            "api_key": self.conf.get("api_key")  # Config parameters which are declared in integration.json are available in the self.conf dict
        }
