package hr.show.service.impl;

import hr.show.configuration.FileProperties;
import hr.show.dto.ImageDto;
import hr.show.exception.NoEntityException;
import hr.show.model.Image;
import hr.show.model.TextCorrection;
import hr.show.repository.ImageRepository;
import hr.show.repository.TextCorrectionRepository;
import hr.show.service.ImageService;
import hr.show.util.ImageUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Optional;

@Service
public class ImageServiceImpl implements ImageService {

    private final ImageRepository imageRepository;
    private final TextCorrectionRepository textCorrectionRepository;
    private final String filePath;

    @Autowired
    public ImageServiceImpl(ImageRepository imageRepository, TextCorrectionRepository textCorrectionRepository, FileProperties fileProperties) {
        this.imageRepository = imageRepository;
        this.textCorrectionRepository = textCorrectionRepository;
        this.filePath = fileProperties.getPath();
    }

    @Override
    public void saveImage(ImageDto imageDto) {
        // save file to file system
        String savePath = writeImage(imageDto.getFile(),ImageUtil.joinDirAndFilePaths(filePath, ImageUtil.getCurrentDayDirName()), imageDto.getId());
        // map
        Image image = new Image();
        image.setId(imageDto.getId());
        image.setCreationTimestamp(imageDto.getCreationDate());
        image.setPath(savePath);
        // save to db
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
    public String writeImage(BufferedImage image, String dirPath, String fileName) {
        try {
            String path = ImageUtil.joinDirAndFilePaths(dirPath, fileName + ".jpg");
            ImageIO.write(image, "jpg", new File(path));
            return path;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
