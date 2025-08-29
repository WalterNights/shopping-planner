import { routes } from './app.routes';
import { provideRouter } from '@angular/router';
import { tokenInterceptor } from './auth/token.interceptor';
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }), 
    provideRouter(routes),
    provideHttpClient(withInterceptorsFromDi()),
    {
      provide: HTTP_INTERCEPTORS,
      useClass: tokenInterceptor,
      multi: true
    }
  ]
};