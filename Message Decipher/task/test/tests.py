from hstest import StageTest, CheckResult, dynamic_test, TestedProgram


class Feedback:
    contain_msg = "Your output should contain the secret message."
    file_not_found_msg = "File not found:"
    read_end_msg = "After reading the file, your output should contain the message:"


class MessageDecipherTest(StageTest):
    read_end_msg = "Finished reading the file"
    secret_message_path = "secret-message.txt"

    @classmethod
    def read_file(cls, path):
        try:
            with open(path, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return False

    @dynamic_test
    def test1(self):
        main = TestedProgram(self.source_name)
        file_output = self.read_file(self.secret_message_path)
        output = main.start()

        # test if the file exists
        if not file_output:
            return CheckResult.wrong(Feedback.file_not_found_msg + f" {self.secret_message_path}")

        # test if the output is correct
        if file_output.strip() not in output.strip():
            return CheckResult.wrong(Feedback.contain_msg)

        # test if the message is correct
        if self.read_end_msg not in output.strip():
            return CheckResult.wrong(Feedback.read_end_msg + f" '{self.read_end_msg}'")

        return CheckResult.correct()


if __name__ == '__main__':
    MessageDecipherTest('task').run_tests()
