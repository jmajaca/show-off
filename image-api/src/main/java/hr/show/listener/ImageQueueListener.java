package hr.show.listener;

import hr.show.message.ImageBoxDataQueueMessage;
import hr.show.message.TextCorrectionQueueMessage;
import hr.show.exception.InvalidImageDataQueueMessage;
import hr.show.service.ImageService;
import io.opentracing.*;
import io.opentracing.propagation.Format;
import io.opentracing.propagation.TextMap;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import javax.validation.Valid;
import java.util.List;

@Component
public class ImageQueueListener {

    private final static Logger log = LoggerFactory.getLogger(ImageQueueListener.class);

    private final ImageService imageService;

    private final Tracer tracer;

    @Autowired
    public ImageQueueListener(ImageService imageService, Tracer tracer) {
        this.imageService = imageService;
        this.tracer = tracer;
    }

    @RabbitListener(queues = "imageQueue")
    public void receiveImage(byte[] image, @Header("request_id") String requestId,
                             @Header("trace") TextMap carrier) {
        Scope scope = activateSpan("receiveImage", carrier);
        log.info("Received image with id '{}' from image queue", requestId);
        try {
            imageService.writeImage(image, requestId);
        } catch (Exception e) {
            log.error("Error has occurred while saving image from queue: ", e);
        }
        scope.close();
    }

    @RabbitListener(queues = "imageDataQueue")
    public void receiveImageData(@Valid List<ImageBoxDataQueueMessage> imageBoxDataMessage,
                                 @Header("request_id") String requestId,
                                 @Header("trace") TextMap carrier) {
        Scope scope = activateSpan("receiveImageData", carrier);
        log.info("Received image data with id '{}' from image queue", requestId);
        try {
            if (requestId == null || requestId.equals("")) {
                throw new InvalidImageDataQueueMessage(requestId);
            }
            imageService.saveDataImage(imageBoxDataMessage, requestId);
        } catch (Exception e) {
            log.error("Error has occurred while saving image data from queue: ", e);
        }
        scope.close();
    }

    @RabbitListener(queues = "textCorrectionQueue")
    public void receiveTextCorrection(@Valid TextCorrectionQueueMessage correctionDto,
                                      @Header("request_id") String requestId,
                                      @Header("trace") TextMap carrier) {
        Scope scope = activateSpan("textCorrectionQueue", carrier);
        log.info("Received text correction for image with id '{}' from text correction queue", correctionDto.getId());
        try {
            imageService.saveTextCorrection(correctionDto.getId(), correctionDto.getText());
        } catch (Exception e) {
            log.error("Error has occurred while saving text correction from queue: ", e);
        }
        scope.close();
    }

    private Scope activateSpan(String operationName, TextMap carrier) {
        SpanContext receivedSpan = tracer.extract(Format.Builtin.TEXT_MAP, carrier);
        Span span = tracer.buildSpan(operationName)
                .addReference(References.FOLLOWS_FROM, receivedSpan)
                .start();
        return tracer.activateSpan(span);
    }

}
