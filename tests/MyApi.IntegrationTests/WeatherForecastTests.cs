using System.Net;
using FluentAssertions;
using Xunit;

namespace MyApi.IntegrationTests;

public class WeatherForecastTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;

    public WeatherForecastTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GET_weatherforecast_returns_200()
    {
        var response = await _client.GetAsync("/WeatherForecast");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}

