package hr.show.service.impl;

import hr.show.configuration.FileProperties;
import hr.show.message.ImageDataQueueMessage;
import hr.show.dto.ImageDto;
import hr.show.exception.NoEntityException;
import hr.show.mapper.ImageDataQueueDtoToImageMapper;
import hr.show.model.Image;
import hr.show.model.TextCorrection;
import hr.show.repository.ImageRepository;
import hr.show.repository.TextCorrectionRepository;
import hr.show.service.ImageService;
import hr.show.util.ImageUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Optional;

@Service
public class ImageServiceImpl implements ImageService {

    private final ImageRepository imageRepository;
    private final TextCorrectionRepository textCorrectionRepository;

    private final ImageDataQueueDtoToImageMapper imageDataQueueDtoToImageMapper;

    private final String filePath;

    private static final String JPG_EXTENSION = ".jpg";

    @Autowired
    public ImageServiceImpl(ImageRepository imageRepository, TextCorrectionRepository textCorrectionRepository,
                            FileProperties fileProperties, ImageDataQueueDtoToImageMapper imageDataQueueDtoToImageMapper) {
        this.imageRepository = imageRepository;
        this.textCorrectionRepository = textCorrectionRepository;
        this.imageDataQueueDtoToImageMapper = imageDataQueueDtoToImageMapper;
        this.filePath = fileProperties.getPath();
    }

    @Override
    public void saveDataImage(ImageDataQueueMessage imageDataQueueMessage) {
        Image image = imageDataQueueDtoToImageMapper.map(imageDataQueueMessage);
        image.setPath(ImageUtil.joinDirAndFilePaths(filePath, ImageUtil.getCurrentDayDirName(), imageDataQueueMessage.getId() + JPG_EXTENSION));
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
        String path = ImageUtil.joinDirAndFilePaths(filePath, ImageUtil.getCurrentDayDirName(), requestId + JPG_EXTENSION);
        try (FileOutputStream stream = new FileOutputStream(path)) {
            stream.write(image);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
