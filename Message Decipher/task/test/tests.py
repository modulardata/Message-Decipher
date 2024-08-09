import re
import string

from hstest import StageTest, CheckResult, dynamic_test, TestedProgram


class Feedback:
    contain_msg = "Your new file should contain the decoded message."
    file_not_found_msg = "File not found: "
    read_end_msg = "After reading the file, your output should contain the message: "
    write_end_msg = "After writing the file, your output should contain the message: "


class MessageDecipherTest(StageTest):
    write_end_msg = "Finished writing the file"
    decode_end_msg = "Finished decoding the file"
    secret_message_path = "secret-message.txt"
    decoded_path = "decoded-message.txt"
    letters = list(string.ascii_lowercase)
    reversed_letters = letters[::-1]

    @classmethod
    def read_file(cls, path):
        try:
            with open(path, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return False

    @classmethod
    def replacer(cls, char):
        i = cls.reversed_letters.index(char.lower())
        return cls.letters[i]

    @classmethod
    def decode_message(cls):
        chunk = cls.read_file(cls.secret_message_path)
        if not chunk:
            return False

        output = re.sub(r'[a-zA-Z]', lambda x: cls.replacer(x.group()), chunk)
        return output

    @dynamic_test
    def test1(self):
        main = TestedProgram(self.source_name)
        file_output = self.decode_message()
        output = main.start()

        # test if the file exists
        if not file_output:
            return CheckResult.wrong(Feedback.file_not_found_msg + self.secret_message_path)

        decoded_output = self.read_file(self.decoded_path)

        # test if the file exists
        if not decoded_output:
            return CheckResult.wrong(Feedback.file_not_found_msg + self.decoded_path)

        # test if the decoded output is correct
        if file_output.strip() not in decoded_output.strip():
            return CheckResult.wrong(Feedback.contain_msg)

        # test if the decode message is correct
        if self.decode_end_msg not in output.strip():
            return CheckResult.wrong(Feedback.read_end_msg + f"'{self.decode_end_msg}'")

        # test if the write message is correct
        if self.write_end_msg not in output.strip():
            return CheckResult.wrong(Feedback.write_end_msg + f"'{self.write_end_msg}'")

        return CheckResult.correct()


if __name__ == '__main__':
    MessageDecipherTest('task').run_tests()
