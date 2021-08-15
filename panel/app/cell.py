
class Container:

    def __init__(self, type, body):
        self._body = body
        self._type = type

    def to_html(self):
        pass

class TextContainer(Container):

    def to_html(self):
        html = f"<div><span class='highlight blue'>{self._body}</span></div>"
        return html


class DataFrameContainer(Container):

    def to_html(self):
        pass
        
class ChartContainer(Container):

    def to_html(self):
        pass
        

class ContainerFactory:

    @classmethod
    def from_type(cls, body):
        if type == "text":
            return TextContainer(body)
        if type == "dataframe":
            return DataFrameContainer(body)
        if type == "chart":
            return ChartContainer(body)

class Cell:

    def __init__(self, body, type):
        self._container = ContainerFactory.make(type, body)

    def to_html(self) -> str:
        self._container.to_html()
