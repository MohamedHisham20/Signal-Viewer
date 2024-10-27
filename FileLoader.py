from Signal import Signal
import os


class SignalsLoader:
    @staticmethod
    def load_file(file_path):
        signal = Signal.from_file(file_path)
        if signal:
            signal.label = file_path.split('/')[-1].split('.')[0]
        return signal

    @staticmethod
    def load_directory(directory_path):
        signals = []
        for file_name in os.listdir(directory_path):
            if file_name.endswith('.csv'):
                file_path = os.path.join(directory_path, file_name)
                signal = Signal.from_file(file_path)
                if signal:
                    signal.label = file_name.split('/')[-1].split('.')[0]
                    signals.append(signal)
        return signals
