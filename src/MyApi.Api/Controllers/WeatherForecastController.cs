using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MyApi.Api.Data;
using MyApi.Api.Domain;
using MyApi.Api.Entities;

namespace MyApi.Api.Controllers;

[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{
    private readonly ApplicationDbContext _db;

    public WeatherForecastController(ApplicationDbContext db)
    {
        _db = db;
    }

    [HttpGet]
    public async Task<IEnumerable<WeatherForecastEntity>> Get()
    {
        var forecasts = await _db.WeatherForecasts.ToListAsync();

        return forecasts.Select(f => new WeatherForecastEntity(
            f.Date,
            f.TemperatureC,
            f.Summary
        ));
    }

    [HttpPost]
    public async Task<IActionResult> Create(WeatherForecastEntity forecast)
    {
        var entity = new WeatherForecast
        {
            Date = forecast.Date,
            TemperatureC = forecast.TemperatureC,
            Summary = forecast.Summary
        };

        _db.WeatherForecasts.Add(entity);
        await _db.SaveChangesAsync();

        return Ok();
    }
}
