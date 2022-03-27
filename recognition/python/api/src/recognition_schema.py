from marshmallow import Schema, fields


class ExtractRequestSchema(Schema):

    imageN = fields.Raw(metadata={'description': 'Image in bytes where N represents positive integer number'})


class ExtractResponseSchema(Schema):

    tokens = fields.List(fields.String(), metadata={'description': 'Extracted texts from images'})


class ErrorSchema(Schema):

    timestamp = fields.DateTime(metadata={'description': 'Timestamp of when error occurred'})
    error = fields.Str(metadata={'description': 'Error description'})
