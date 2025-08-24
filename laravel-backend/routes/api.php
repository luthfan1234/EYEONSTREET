<?php

use App\Http\Controllers\Api\IncidentController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// Rute-rute yang boleh diakses secara publik (tanpa login)
// Python script dan halaman dashboard bisa mengakses ini.
Route::get('/incidents', [IncidentController::class, 'index']);
Route::post('/incidents', [IncidentController::class, 'store']);


// Rute yang hanya bisa diakses oleh pengguna yang sudah login
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});
