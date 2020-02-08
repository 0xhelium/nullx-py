import string
import nullx.log as log
from nullx.crypto.__base import Cipher, CipherCracker

class ShiftException(Exception):
    pass
class UnknownShiftCipher(Exception):
    pass
class ShiftCipherCrackError(Exception):
    pass
class FrequencyAnalysisError(Exception):
    pass

class Shift(Cipher):
    def __init__(self, char_set=string.ascii_uppercase, ignore_case=True, ignore_unknown_characters=True, keep_case=True):
        self.char_set = char_set
        self.ignore_case = ignore_case
        self.ignore_unknown_characters = ignore_unknown_characters
        self.keep_case = keep_case
    
    def _handle_unknown_character(self, char):
        if self.ignore_unknown_characters:
            return True
        else:
            log.throw(ShiftException("Nullx: Unrecognized character '" + char + "'"))
    
    def _nhouc_char_index(self, char, ignore_case):
        try:
            i = self.char_set.index(char)
        except ValueError:
            if ignore_case:
                try:
                    i = self.char_set.index(char.swapcase())
                except ValueError:
                    raise ShiftException("Unrecognized character")
            else:
                raise ShiftException("Unrecognized character")
        return i

    def _char_index(self, char, ignore_case):
        try:
            return self._nhouc_char_index(char, ignore_case)
        except ShiftException:
            if self._handle_unknown_character(char):
                return None
    
    def _shift_char(self, char, shift_n):
        char_index = self._char_index(char, self.ignore_case)
        if char_index is None:
            return None
        shifted_char = self.char_set[(char_index + shift_n) % len(self.char_set)]
        if self.keep_case:
            return shifted_char.upper() if char.isupper() else shifted_char.lower()
        else:
            return shifted_char

    def encrypt(self, x, shift_n):
        pass

    def decrypt(self, x, shift_n):
        pass

class Caesar(Shift):
    def _shift(self, x, shift_n):
        shifted = ""
        for char in x:
            shifted_char = self._shift_char(char, shift_n)
            shifted += shifted_char if shifted_char is not None else char
        return shifted

    def encrypt(self, x, shift_n):
        return self._shift(x, shift_n)

    def decrypt(self, x, shift_n):
        if isinstance(shift_n, FrequencyAnalyzer):
            log.info("Nullx: Starting cracker " + shift_n.__class__.__name__)
            shift_n = shift_n.run(x)
        elif isinstance(shift_n, CipherCracker):
            log.throw(ShiftCipherCrackError("Nullx: Incompatible cipher cracker '" + shift_n.__name__ + "'\nCompatible cipher crackers: FrequencyAnalyzer"))
        return self._shift(x, -shift_n)

class Polynumeric(Shift):
    def _shift(self, x, shift_ns, reverse=False):
        shifted = ""
        bad_chars = 0
        for i in range(len(x)):
            shift_n = shift_ns[(i - bad_chars) % len(shift_ns)]
            shifted_char = self._shift_char(x[i], shift_n if not reverse else -shift_n)
            if shifted_char is not None:
                shifted += shifted_char
            else:
                bad_chars += 1
                shifted += x[i]
        return shifted

    def encrypt(self, x, key):
        return self._shift(x, key)

    def decrypt(self, x, key):
        if isinstance(key, PolynumericFrequencyAnalyzer):
            key = key.run(x)
        elif isinstance(key, CipherCracker):
            log.throw(ShiftCipherCrackError("Nullx: Incompatible cipher cracker '" + key.__name__ + "'\nCompatible cipher crackers: PolynumericFrequencyAnalyzer"))
        return self._shift(x, key, reverse=True)

class Polyalphabetic(Polynumeric):
    def __init__(self, char_set=string.ascii_uppercase, ignore_case=True, ignore_key_case=True, ignore_unknown_characters=True, keep_case=True):
        super().__init__(char_set=char_set, ignore_case=ignore_case, ignore_unknown_characters=ignore_unknown_characters, keep_case=keep_case)
        self.ignore_key_case = ignore_key_case

    def _key_to_indices(self, key):
        key_positions = []
        for char in key:
            try:
                key_positions.append(self._nhouc_char_index(char, self.ignore_key_case))
            except ShiftException:
                log.throw(ShiftException("Nullx: Unrecognized character '" + char + "' in key"))
        return key_positions

    def _shift(self, x, key, reverse=False):
        key_positions = self._key_to_indices(key)
        return super()._shift(x, key_positions, reverse=reverse)
    
    def decrypt(self, x, key):
        if isinstance(key, PolyalphabeticFrequencyAnalyzer):
            key = key.run(x)
        elif isinstance(key, CipherCracker):
            log.throw(ShiftCipherCrackError("Nullx: Incompatible cipher cracker '" + key.__name__ + "'\nCompatible cipher crackers: PolyalphabeticFrequencyAnalyzer"))
        return super().decrypt(x, key)
    
Vigenère = Vigenere = Polyalphabetic

class FrequencyDefinition:
    def __init__(self, chars, frequencies):
        self.chars = chars
        self.frequencies = frequencies
    
    def getFrequency(self, char):
        return self.frequencies[self.chars.index(char)]

class FrequencyCalculator:
    def __init__(self, chars, ignore_case=True, ignore_unknown_characters=True):
        self.frequency_definition = FrequencyDefinition(chars, None)
        self.occurrences = [0] * len(chars)
        self.ignore_case = ignore_case
        self.ignore_unknown_characters = ignore_unknown_characters
    
    def _handle_unknown_character(self, char):
        if self.ignore_unknown_characters:
            return True
        else:
            log.throw(FrequencyAnalysisError("Nullx: Unrecognized character'" + char + "'"))
    
    def calc(self, x):
        for char in x:
            try:
                i = self.frequency_definition.chars.index(char)
            except ValueError:
                if self.ignore_case:
                    try:
                        i = self.frequency_definition.chars.index(char.swapcase())
                    except ValueError:
                        if self._handle_unknown_character(char):
                            continue
                else:
                    if self._handle_unknown_character(char):
                        continue
            self.occurrences[i] += 1
        self.frequency_definition.frequencies = [(oc / len(x)) * 100.0 for oc in self.occurrences]
        return self.frequency_definition

_ENGLISH_FREQUENCY = FrequencyDefinition(
    ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"],
    [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.36,0.15,1.974,0.074]
)
class FrequencyAnalyzer(CipherCracker):
    ENGLISH_FREQUENCY = _ENGLISH_FREQUENCY
    def __init__(self, frequency_definition=_ENGLISH_FREQUENCY, ignore_case=True, ignore_unknown_characters=True):
        self.frequency_definition = frequency_definition
        self.ignore_case = ignore_case
        self.ignore_unknown_characters = ignore_unknown_characters
    
    def _calc_shift(self, expected, actual):
        shifts = [[i, 0.0] for i in range(len(expected.chars))]
        for i in range(len(expected.chars)):
            total = 0.0
            for j in range(len(expected.frequencies)):
                e = expected.frequencies[j]
                a = actual.frequencies[(j + i) % len(expected.chars)]
                total += (a - e) ** 2
            shifts[i][1] = total / len(expected.frequencies)
        shifts = sorted(shifts, key=lambda x: x[1])
        return [s[0] for s in shifts]
    
    def run(self, x):
        frequency_calculator = FrequencyCalculator(self.frequency_definition.chars, ignore_case=self.ignore_case, ignore_unknown_characters=self.ignore_unknown_characters)
        in_freq_def = frequency_calculator.calc(x)
        shifts = self._calc_shift(self.frequency_definition, in_freq_def)
        log.ll(
            info="Nullx: Frequency analysis done. Best matching shift: " + str(shifts[0]),
            verbose="Nullx: Frequency analysis done. Shifts in order from best match to worst match:\n" + ", ".join([str(s) for s in shifts])
        )
        return shifts[0]

class PolynumericFrequencyAnalyzer(FrequencyAnalyzer):
    def __init__(self, key_length, frequency_definition=_ENGLISH_FREQUENCY, ignore_case=True, ignore_unknown_characters=True):
        super().__init__(frequency_definition=frequency_definition, ignore_case=ignore_case, ignore_unknown_characters=ignore_unknown_characters)
        self.key_length = key_length
    
    def _group(self, x):
        groups = [""] * self.key_length
        bad_chars = 0
        for i in range(len(x)):
            if x[i] not in self.frequency_definition.chars:
                if self.ignore_case:
                    if x[i].swapcase() not in self.frequency_definition.chars:
                        if self.ignore_unknown_characters:
                            bad_chars += 1
                            continue
                        else:
                            log.throw(FrequencyAnalysisError("Nullx: Unrecognized character '" + x[i] + "'"))
            groups[(i - bad_chars) % self.key_length] += x[i]
        return groups
    
    def _calc_key(self, x):
        groups = self._group(x)
        freq_calc = FrequencyCalculator(self.frequency_definition.chars, ignore_case=self.ignore_case, ignore_unknown_characters=self.ignore_unknown_characters)
        shifts = [[]] * len(self.frequency_definition.chars)
        for g in groups:
            group_freq_def = freq_calc.calc(g)
            predicted_shifts = self._calc_shift(self.frequency_definition, group_freq_def)
            for i in range(len(predicted_shifts)):
                shifts[i].append(predicted_shifts[i])
        return shifts[0]
    
    def run(self, x):
        return self._calc_key(x)

class PolyalphabeticFrequencyAnalyzer(PolynumericFrequencyAnalyzer):
    def run(self, x):
        return [self.frequency_definition.chars[s] for s in super().run(x)]
