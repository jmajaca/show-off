package hr.show.configuration;

import hr.show.log.CustomHttpLogFormatter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.util.StringUtils;
import org.zalando.logbook.DefaultHttpLogWriter;
import org.zalando.logbook.DefaultSink;
import org.zalando.logbook.Logbook;

import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import static org.zalando.logbook.HeaderFilters.authorization;

// https://github.com/zalando/logbook
@Configuration
public class LogbookConfiguration {

    private static final List<String> allowedHeaders = List.of(HttpHeaders.AUTHORIZATION);

    @Bean
    public Logbook logbook() {
        return Logbook.builder()
                .headerFilter(headers -> {
                    List<String> headersToDelete = new LinkedList<>();
                    for (Map.Entry<String, ?> entry : headers.entrySet()) {
                        if(!allowedHeaders.contains(StringUtils.capitalize(entry.getKey()))) {
                            headersToDelete.add(entry.getKey());
                        }
                    }
                    return headers.delete(headersToDelete);
                })
                .headerFilter(authorization())
                .sink(new DefaultSink(new CustomHttpLogFormatter(), new DefaultHttpLogWriter()))
                .build();
    }

}
