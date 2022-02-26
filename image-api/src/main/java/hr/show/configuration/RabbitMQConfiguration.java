package hr.show.configuration;

import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;

public class RabbitMQConfiguration {

    @Bean
    public Queue imageQueue() {
        return new Queue("image-queue");
    }

    @Bean
    public Queue textCorrectionQueue() {
        return new Queue("text-correction");
    }

}
