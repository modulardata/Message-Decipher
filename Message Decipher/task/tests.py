import re
import string

from hstest import StageTest, CheckResult, dynamic_test, TestedProgram


class Feedback:
    contain_msg = "Your new file should contain the decoded message."
    file_not_found_msg = "File not found: "
    read_end_msg = "After reading the file, your output should contain the message: "
    write_end_msg = "After writing the file, your output should contain the message: "
    wait_input = "Your program should ask for a shift value."
    encode_contain_msg = "Your new file should contain the encoded message."


class MessageDecipherTest(StageTest):
    encode_end_msg = "Finished encoding the file"
    write_end_msg = "Finished writing the file"
    decode_end_msg = "Finished decoding the file"

    secret_message_path = "secret-message.txt"
    decoded_path = "decoded-message.txt"
    message_path = "message.txt"
    encoded_path = "encoded-message.txt"

    letters = list(string.ascii_lowercase)
    reversed_letters = letters[::-1]
    shift_letters = []

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
        replaced_char = cls.letters[i]
        return replaced_char.upper() if char.isupper() else replaced_char

    @classmethod
    def decode_message(cls):
        chunk = cls.read_file(cls.secret_message_path)
        if not chunk:
            return False

        output = re.sub(r'[a-zA-Z]', lambda x: cls.replacer(x.group()), chunk)
        return output

    @classmethod
    def shift_replacer(cls, char):
        i = cls.letters.index(char.lower())
        replaced_char = cls.shift_letters[i]
        return replaced_char.upper() if char.isupper() else replaced_char

    @classmethod
    def encode_message(cls, shift):
        cls.shift_letters = list(map(lambda x: cls.letters[(cls.letters.index(x) + shift) % len(cls.letters)],
                                     cls.letters))

        chunk = cls.read_file(cls.message_path)
        if not chunk:
            return False

        output = re.sub(r'[a-zA-Z]', lambda x: cls.shift_replacer(x.group()), chunk)
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

    @dynamic_test(data=["3", "5"])
    def test2(self, shift):
        main = TestedProgram(self.source_name)
        file_output = self.encode_message(int(shift))
        main.start()

        if main.is_waiting_input():
            output = main.execute(shift)

            # test if the file exists
            if not file_output:
                return CheckResult.wrong(Feedback.file_not_found_msg + self.message_path)

            encoded_output = self.read_file(self.encoded_path)

            # test if the file exists
            if not encoded_output:
                return CheckResult.wrong(Feedback.file_not_found_msg + self.encoded_path)

            # test if the encoded output is correct
            if file_output.strip() not in encoded_output.strip():
                return CheckResult.wrong(Feedback.encode_contain_msg)

            # test if the encode message is correct
            if self.encode_end_msg not in output.strip():
                return CheckResult.wrong(Feedback.read_end_msg + f"'{self.encode_end_msg}'")

            # test if the write message is correct
            if self.write_end_msg not in output.strip():
                return CheckResult.wrong(Feedback.write_end_msg + f"'{self.write_end_msg}'")
            return CheckResult.correct()

        else:
            return CheckResult.wrong(Feedback.wait_input)


if __name__ == '__main__':
    MessageDecipherTest('task').run_tests()
