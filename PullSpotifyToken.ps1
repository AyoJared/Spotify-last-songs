get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
}


$clientId = $env:client_id
$clientSecret = $env:client_secret

$headers = @{
    "Content-Type" = "application/x-www-form-urlencoded"
}
$body = @{
    grant_type    = "client_credentials"
    client_id     = $clientId
    client_secret = $clientSecret
}

$response = Invoke-RestMethod -Method Post -Uri "https://accounts.spotify.com/api/token" -Headers $headers -Body $body

# Print full token without truncation
$response.access_token

$key = "API_KEY"
$value = $response.access_token
$output = "$key=$value"
Set-Content -Path ".env" -Value $output