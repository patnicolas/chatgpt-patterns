__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import pandas as pd
from util.ioutil import IOUtil


class LLMFineTuning(object):
    prompt_delimiter = '\n\n###\n\n'
    completion_delimiter = '###'

    def __init__(self, training_file: str, validation_file: str):
        self.df_train_set = LLMFineTuning.__add_delimiters(training_file)
        if validation_file:
            self.df_valid_set = LLMFineTuning.__add_delimiters(validation_file)

    def __getitem__(self, items: tuple) -> (str, str):
        if items[0] == 'training':
            return self.df_train_set['prompt'][items[1]], self.df_train_set['completion'][items[1]] \
                if items[1] < len(self.df_train_set) \
                else None
        else:
            return self.df_valid_set['prompt'][items[1]], self.df_valid_set['completion'][items[1]] \
                if items[1] < len(self.df_valid_set) \
                else None

    @staticmethod
    def __add_delimiters(training_file: str) -> pd.DataFrame:
        ioUtil = IOUtil(training_file)
        raw_entry = ioUtil.from_json()
        df = pd.DataFrame(raw_entry, columns=['prompt', 'completion'])
        for index in range(len(df)):
            raw_prompt = df.at[index, 'prompt']
            var = df.at[index, 'prompt'] = f'{raw_prompt} {LLMFineTuning.prompt_delimiter}'
            raw_completion = df.at[index, 'completion']
            df.at[index, 'completion'] = f'{raw_completion} {LLMFineTuning.completion_delimiter}'
        return df


if __name__ == '__main__':
    training_test_file = "../input/train_test.json"
    validation_test_file = "../input/valid_test.json"

    chat_gpt_fine_tuning = LLMFineTuning(training_test_file, validation_test_file)
    training_set_row = chat_gpt_fine_tuning[('training', 2)]
    print(str(training_set_row))
