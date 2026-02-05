using FluentAssertions;
using System.Net;

namespace MyApi.IntegrationTests;

public class WeatherForecastTests
    : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;

    public WeatherForecastTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Trait("Category", "Integration")]
    [Fact]
    public async Task GET_weatherforecast_returns_200()
    {
        var response = await _client.GetAsync("/weatherforecast");

        response.StatusCode.Should().Be(HttpStatusCode.OK);
    }
}
