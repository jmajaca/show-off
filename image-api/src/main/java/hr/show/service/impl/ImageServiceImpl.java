package hr.show.service.impl;

import hr.show.configuration.FileProperties;
import hr.show.mapper.ImageBoxDataQueueDtoToImageBoxMapper;
import hr.show.message.ImageBoxDataQueueMessage;
import hr.show.dto.ImageDto;
import hr.show.exception.NoEntityException;
import hr.show.model.Image;
import hr.show.model.TextCorrection;
import hr.show.repository.ImageRepository;
import hr.show.repository.TextCorrectionRepository;
import hr.show.service.ImageService;
import hr.show.util.ImageUtil;
import io.opentracing.Scope;
import io.opentracing.Span;
import io.opentracing.Tracer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.FileOutputStream;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.LinkedList;
import java.util.List;
import java.util.Optional;

@Service
public class ImageServiceImpl implements ImageService {

    private final ImageRepository imageRepository;
    private final TextCorrectionRepository textCorrectionRepository;

    private final ImageBoxDataQueueDtoToImageBoxMapper imageBoxDataQueueDtoToImageBoxMapper;

    private final Tracer tracer;

    private final String filePath;

    private static final String JPG_EXTENSION = ".jpg";

    @Autowired
    public ImageServiceImpl(ImageRepository imageRepository, TextCorrectionRepository textCorrectionRepository,
                            FileProperties fileProperties, ImageBoxDataQueueDtoToImageBoxMapper imageBoxDataQueueDtoToImageBoxMapper,
                            Tracer tracer) {
        this.imageRepository = imageRepository;
        this.textCorrectionRepository = textCorrectionRepository;
        this.imageBoxDataQueueDtoToImageBoxMapper = imageBoxDataQueueDtoToImageBoxMapper;
        this.filePath = fileProperties.getPath();
        this.tracer = tracer;
    }

    @Override
    public void saveDataImage(List<ImageBoxDataQueueMessage> imageBoxDataQueueMessage, String requestId) {
        Image image = createImage(requestId);
        imageBoxDataQueueMessage.forEach(imageBoxDataQueueDto -> image.getBoxes().add(imageBoxDataQueueDtoToImageBoxMapper.map(imageBoxDataQueueDto)));
        image.getBoxes().forEach(box -> box.setImage(image));
        image.setPath(ImageUtil.joinDirAndFilePaths(filePath, ImageUtil.getCurrentDayDirName(), requestId + JPG_EXTENSION));
        imageRepository.saveAndFlush(image);
    }

    @Override
    public Optional<ImageDto> getImage(String imageId) {
        throw new NoEntityException(Image.class, imageId);
    }

    @Override
    public void saveTextCorrection(String imageId, String value) {
        TextCorrection textCorrection = new TextCorrection();
        textCorrection.setValue(value);
        textCorrection.setImage(imageRepository.getById(imageId));
        textCorrectionRepository.saveAndFlush(textCorrection);
    }

    @Override
    public void writeImage(byte[] image, String requestId) {
        Span span = tracer.buildSpan("writeImage").start();
        try(Scope ignored = tracer.activateSpan(span)) {
            String path = ImageUtil.joinDirAndFilePaths(filePath, ImageUtil.getCurrentDayDirName(), requestId + JPG_EXTENSION);
            try (FileOutputStream stream = new FileOutputStream(path)) {
                stream.write(image);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        } finally {
            span.finish();
        }
    }

    private Image createImage(String requestId) {
        Image image = new Image();
        image.setId(requestId);
        image.setCreationTimestamp(LocalDateTime.now());
        image.setBoxes(new LinkedList<>());
        return image;
    }
}
