package hr.show.listener;

import hr.show.dto.ImageDto;
import hr.show.dto.TextCorrectionDto;
import hr.show.service.ImageService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
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
    public void receiveImage(@Valid ImageDto image) {
        log.info("Received image with id '{}' from image queue", image.getId());
        try {
            imageService.saveImage(image);
        } catch (Exception e) {
            log.error("Error has occurred while saving image from queue: ", e);
        }
    }

    @RabbitListener(queues = "textCorrectionQueue")
    public void receiveTextCorrection(@Valid TextCorrectionDto correctionDto) {
        log.info("Received text correction for image with id '{}' from text correction queue", correctionDto.getImageId());
        try {
            imageService.saveTextCorrection(correctionDto.getImageId(), correctionDto.getValue());
        } catch (Exception e) {
            log.error("Error has occurred while saving text correction from queue: ", e);
        }
    }

}
