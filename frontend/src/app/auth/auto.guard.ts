import { Injectable } from "@angular/core";
import { AuthService } from "./auth.service";
import { CanActivate, Router } from "@angular/router";

@Injectable({
  providedIn: 'root'
})

export class AutoGuard implements CanActivate {
  constructor(private auhtService: AuthService, private router: Router) { }
  canActivate(): boolean {
    if (this.auhtService.isAuthenticated()) {
      return true;
    } else {
      this.router.navigate(['/auth/login']);
      return false;
    }
  }
}