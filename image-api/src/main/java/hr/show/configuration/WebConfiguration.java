package hr.show.configuration;

// https://huchdadiya.medium.com/restful-api-documentation-with-enunciate-3fa2a1a5d8c9
// https://stackoverflow.com/questions/21123437/how-do-i-use-spring-boot-to-serve-static-content-located-in-dropbox-folder

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void addResourceHandlers (ResourceHandlerRegistry registry) {
        String projectPath = System.getProperty("user.dir") + "/image-api";
        registry.addResourceHandler("/docs/**").
                addResourceLocations(String.format("file:%s/build/enunciate/docs/", projectPath));
        registry.addResourceHandler("/**").
                addResourceLocations(String.format("file:%s/build/enunciate/docs/", projectPath));
    }

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        registry.addViewController("/docs").setViewName("forward:/docs/index.html");
    }
}
