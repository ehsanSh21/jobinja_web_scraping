import re

class Convertor:
    def add(self, x, y):
        return x + y
    

    def get_province(self, input_string):
        parts = input_string.split('،')
        if len(parts) > 0:
            return parts[0].strip()
        return None

    def get_city(self, input_string):
        parts = input_string.split('،')
        if len(parts) > 1:
            return parts[1].strip()
        return None


    def extract_span_text(self, spans):
         text_array = []
         for span in spans:
            text_array.append(span.text)
         return text_array


    def extract_english_phrase(self,text):
        # Match the English phrase outside parentheses or the entire phrase inside parentheses
        match = re.search(
            r'(?<=\()\s*([A-Za-z.+#]+(?:\s*[-\s]*[A-Za-z.+#]+)*)\s*(?=\))|([A-Za-z.+#]+(?:\s*[-\s]*[A-Za-z.+#]+)*)',
            text)

        if match:
            return match.group(1) or match.group(2)
        else:
            return text