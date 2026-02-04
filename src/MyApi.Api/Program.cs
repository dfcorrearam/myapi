using Microsoft.EntityFrameworkCore;
using MyApi.Api.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

// Configurar DbContext
if (builder.Environment.IsDevelopment())
{
    // Desarrollo local → SQLite
    builder.Services.AddDbContext<ApplicationDbContext>(options =>
        options.UseSqlite("Data Source=MyApiDb.db"));
}
else
{
    // Producción / CI → SQL Server (usando variable de entorno)
    var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
    builder.Services.AddDbContext<ApplicationDbContext>(options =>
        options.UseSqlServer(connectionString));
}

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseAuthorization();
app.MapControllers();

app.Run();

public partial class Program { }

