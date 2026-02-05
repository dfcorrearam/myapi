using FluentAssertions;
using MyApi.Api.Domain;

namespace MyApi.Api.UnitTests;

public class WeatherForecastEntityTests
{
    [Fact]
    public void Should_create_weather_forecast_entity()
    {
        var date = DateTime.UtcNow;
        var temperature = 25;
        var summary = "Sunny";

        var entity = new WeatherForecastEntity(date, temperature, summary);

        entity.Date.Should().Be(date);
        entity.TemperatureC.Should().Be(temperature);
        entity.Summary.Should().Be(summary);
    }
}
