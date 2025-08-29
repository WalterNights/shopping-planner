import { Routes } from '@angular/router';
import { AutoGuard } from './auth/auto.guard';

export const routes: Routes = [
    // Component Paths
    { path: '', loadComponent: () => import('./home/home.component').then(m =>m.HomeComponent) },

    // Authorization Paths
    { path: 'auth', loadChildren: () => import('./auth/auth.module').then(m => m.AuthModule) },
    { path: '**', redirectTo: 'auth/register' },
];