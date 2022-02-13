from marshmallow import Schema, fields


class PointSchema(Schema):

    axis_x = fields.Int()
    axis_y = fields.Int()


class TextBoxSchema(Schema):

    ord_num = fields.Int()
    points = fields.List(fields.Nested(PointSchema))
    probability = fields.Float()


class MinimalTextBoxSchema(Schema):

    start_x: fields.Int()
    start_y: fields.Int()
    width: fields.Int()
    height: fields.Int()
