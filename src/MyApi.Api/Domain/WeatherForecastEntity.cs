namespace MyApi.Api.Domain;

public record WeatherForecastEntity(
    DateTime Date,
    int TemperatureC,
    string? Summary
);
