from marshmallow import Schema, fields


class PointSchema(Schema):

    axis_x = fields.Int(metadata={'description': 'x-axis coordinate of point'})
    axis_y = fields.Int(metadata={'description': 'y-axis coordinate of point'})


class TextBoxRequestSchema(Schema):

    image = fields.Raw(metadata={'description': 'Image in bytes'})


class TextBoxSchema(Schema):

    ord_num = fields.Int(metadata={'description': 'Ordinal number of box'})
    points = fields.List(fields.Nested(PointSchema), metadata={'description': 'Points that determine box'})
    probability = fields.Float(metadata={'description': 'Probability of box containing text'})


class MinimalTextBoxSchema(Schema):

    start_x = fields.Int(metadata={'description': 'x-axis coordinate of the starting point of the box'})
    start_y = fields.Int(metadata={'description': 'y-axis coordinate of the starting point of the box'})
    width = fields.Int(metadata={'description': 'width of the text box'})
    height = fields.Int(metadata={'description': 'height of the text box'})


class ErrorSchema(Schema):

    timestamp = fields.DateTime(metadata={'description': 'Timestamp of when error occurred'})
    error = fields.Str(metadata={'description': 'Error description'})
