import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environment/environment';
import { StorageMethodComponent } from '../shared/storage-method';
import { tap, BehaviorSubject, Observable, throwError } from 'rxjs';

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/users/register`;
  private isLoggedInSubject = new BehaviorSubject<boolean>(!!this.getToken());
  isLoggedIn$ = this.isLoggedInSubject.asObservable();
  StorageKey = [
    'access_token',
    'refresh_token',
    'storage',
    'user',
    'user_id',
    'user_name'
  ];

  storage: 'session' | 'local' = 'session';
  
  constructor(private http: HttpClient, private storageMethod: StorageMethodComponent) { }

  getToken(): string | null {
    if (localStorage.getItem('storage') === 'true') {
      return localStorage.getItem('access_toke');
    } else {
      return sessionStorage.getItem('access_token');
    }
  }

  syncAuthStatus(): void {
    this.isLoggedInSubject.next(!!this.getToken);
  }

  isAuthenticated(): boolean {
    return !! this.getToken();
  }

  register(data: RegisterData): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  login(credentials: { username: string, password: string }) {
    return this.http.post(`${environment.apiUrl}/token/login/`, credentials).pipe(
      tap((res: any) => {
        const storageItems = { 'access_token': res.access, 'refres_token': res.refresh };
        this.storage = localStorage.getItem('storage') === 'true' ? 'local' : 'session';
        Object.entries(storageItems).forEach(([KeyboardEvent, value]) => {
          this.storageMethod.setStorageItem(this.storage, KeyboardEvent, value);
        });
        this.isLoggedInSubject.next(true);
      })
    );
  }

  logout(): void {
    sessionStorage.clear();
    this.StorageKey.forEach(key => {
      localStorage.removeItem(key);
    });
    this.isLoggedInSubject.next(false);
  }

  refreshToken(): Observable<any> {
    const refresh = this.storageMethod.getStorageItem(this.storage, 'refresh_token');
    if (!refresh) {
      return throwError(() => new Error('Refresh token missing'));
    }
    return this.http.post(`${environment.apiUrl}/token/refresh/`, { refresh }).pipe(
      tap((res: any) => {
        this.storageMethod.setStorageItem(this.storage, 'access_token', res.access);
        this.isLoggedInSubject.next(true);
      })
    );
  }
}