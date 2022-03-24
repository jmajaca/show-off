package hr.show.listener;

import hr.show.message.ImageDataQueueMessage;
import hr.show.message.TextCorrectionQueueMessage;
import hr.show.exception.InvalidImageDataQueueMessage;
import hr.show.service.ImageService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

import javax.validation.Valid;

@Component
public class ImageQueueListener {

    private final static Logger log = LoggerFactory.getLogger(ImageQueueListener.class);

    private final ImageService imageService;

    @Autowired
    public ImageQueueListener(ImageService imageService) {
        this.imageService = imageService;
    }

    @RabbitListener(queues = "imageQueue")
    public void receiveImage(byte[] image, @Header("request_id") String requestId) {
        log.info("Received image with id '{}' from image queue", requestId);
        try {
            imageService.writeImage(image, requestId);
        } catch (Exception e) {
            log.error("Error has occurred while saving image from queue: ", e);
        }
    }

    @RabbitListener(queues = "imageDataQueue")
    public void receiveImageData(@Valid ImageDataQueueMessage imageDataQueueMessage, @Header("request_id") String requestId) {
        log.info("Received image data with id '{}' from image queue", imageDataQueueMessage.getId());
        try {
            if (!requestId.equals(imageDataQueueMessage.getId())) {
                throw new InvalidImageDataQueueMessage(imageDataQueueMessage.getId(), requestId);
            }
            imageService.saveDataImage(imageDataQueueMessage);
        } catch (Exception e) {
            log.error("Error has occurred while saving image data from queue: ", e);
        }
    }

    @RabbitListener(queues = "textCorrectionQueue")
    public void receiveTextCorrection(@Valid TextCorrectionQueueMessage correctionDto, @Header("request_id") String requestId) {
        log.info("Received text correction for image with id '{}' from text correction queue", correctionDto.getId());
        try {
            imageService.saveTextCorrection(correctionDto.getId(), correctionDto.getText());
        } catch (Exception e) {
            log.error("Error has occurred while saving text correction from queue: ", e);
        }
    }

}
