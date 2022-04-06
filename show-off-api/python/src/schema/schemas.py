from marshmallow import Schema, fields


class ReadImageRequestSchema(Schema):

    image = fields.Raw(metadata={'description': 'Image in bytes'})


class ReadImageResponseSchema(Schema):

    id = fields.Str(metadata={'description': 'Unique identifier of OCR request'})
    text = fields.Str(metadata={'description': 'Extracted text from image'})


class ErrorSchema(Schema):

    timestamp = fields.DateTime(metadata={'description': 'Timestamp of when error occurred'})
    error = fields.Str(metadata={'description': 'Error description'})


class TextCorrectionSchema(Schema):

    id = fields.Str(metadata={'description': 'Unique identifier of OCR request'})
    text = fields.Str(metadata={'description': 'Text correction'})
