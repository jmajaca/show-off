package hr.show.log;

import org.apiguardian.api.API;
import org.zalando.logbook.Correlation;
import org.zalando.logbook.HttpLogFormatter;
import org.zalando.logbook.HttpMessage;
import org.zalando.logbook.HttpRequest;
import org.zalando.logbook.HttpResponse;
import org.zalando.logbook.Origin;
import org.zalando.logbook.Precorrelation;

import java.io.IOException;
import java.util.List;
import java.util.Map;

import static org.apiguardian.api.API.Status.STABLE;

@API(status = STABLE)
public final class CustomHttpLogFormatter implements HttpLogFormatter {

    @Override
    public String format(final Precorrelation precorrelation, final HttpRequest request) throws IOException {
        final String correlationId = precorrelation.getId();
        final String body = request.getBodyAsString();

        final StringBuilder result = new StringBuilder(body.length() + 2048);

        result.append(direction(request));
        result.append(" Request: ");
        result.append(correlationId);
        result.append(", ");

        result.append(request.getRemote());
        result.append(" - ");

        result.append('"');
        result.append(request.getMethod());
        result.append(' ');
        result.append(request.getPath());
        result.append(' ');
        result.append(request.getProtocolVersion());
        result.append('"');
        result.append(" - ");

        writeHeaders(request.getHeaders(), result);
        writeBody(body, result);

        return result.toString();
    }

    @Override
    public String format(final Correlation correlation, final HttpResponse response) throws IOException {
        final String correlationId = correlation.getId();
        final String body = response.getBodyAsString();

        final StringBuilder result = new StringBuilder(body.length() + 2048);

        result.append(direction(response));
        result.append(" Response: ");
        result.append(correlationId);
        result.append(',');
        result.append(" Duration: ");
        result.append(correlation.getDuration().toMillis());
        result.append(" ms, ");

        result.append(response.getProtocolVersion());
        result.append(' ');
        result.append(response.getStatus());
        final String reasonPhrase = response.getReasonPhrase();
        if (reasonPhrase != null) {
            result.append(' ');
            result.append(reasonPhrase);
        }

        result.append(" - ");

        writeHeaders(response.getHeaders(), result);
        writeBody(body, result);

        return result.toString();
    }

    private String direction(final HttpMessage request) {
        return request.getOrigin() == Origin.REMOTE ? "Incoming" : "Outgoing";
    }

    private void writeHeaders(final Map<String, List<String>> headers, final StringBuilder output) {
        if (headers.isEmpty()) {
            return;
        }

        for (final Map.Entry<String, List<String>> entry : headers.entrySet()) {
            output.append(entry.getKey());
            output.append(": ");
            final List<String> headerValues = entry.getValue();
            if (!headerValues.isEmpty()) {
                for (final String value : entry.getValue()) {
                    output.append(value);
                    output.append(", ");
                }
                output.setLength(output.length() - 2); // discard last comma
            }
            output.append(", ");
        }
        output.setLength(output.length() - 1);
    }

    private void writeBody(final String body, final StringBuilder output) {
        if (!body.isEmpty()) {
            output.append("Body: ");
            output.append(body);
        } else {
            output.setLength(output.length() - 1); // discard last newline
        }
    }

}
